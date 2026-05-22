import numpy as np
import random
import math  
from pyscript import document, when # type: ignore
import js # type: ignore
from pyodide.ffi import to_js # type: ignore

class WebLofiEngine:
    def __init__(self, bpm=85):
        self.sr = 44100
        self.bpm = bpm
        self.beat_ms = int(60000 / self.bpm)
        self.last_chord_idx = -1
        self.chords_pool = [
            [261, 329, 392, 493], [349, 440, 523, 659], 
            [293, 349, 440, 587], [392, 493, 587, 739],
            [329, 392, 493, 622]
        ]
        self.current_cfg = {"filter": 400, "noise": 0.002}

    def _gen_drum(self, type="kick"):
        dur = 0.15
        t = np.linspace(0, dur, int(self.sr * dur), False)
        if type == "kick":
            wave = np.sin(2 * np.pi * 60 * np.exp(-15 * t) * t)
        elif type == "snare":
            wave = np.random.normal(0, 0.2, len(t)) * np.exp(-10 * t)
        else: 
            t_hihat = np.linspace(0, 0.05, int(self.sr * 0.05), False)
            wave = np.random.normal(0, 0.1, len(t_hihat))
        return wave

    def _gen_tone(self, freqs, dur_ms, is_melody=False):
        samples = int(self.sr * dur_ms / 1000)
        t = np.linspace(0, dur_ms/1000, samples, False)
        mixed = np.zeros_like(t)
        
        for f in freqs:
            amp = 0.05 if is_melody else 0.15
            mixed += amp * np.sin(2 * np.pi * f * t) * np.exp(-0.8 * t)
        
        fade_in = int(self.sr * 0.01)
        fade_out = int(self.sr * 0.03)
        if len(mixed) > fade_in + fade_out:
            mixed[:fade_in] *= np.linspace(0, 1, fade_in)
            mixed[-fade_out:] *= np.linspace(1, 0, fade_out)
            
        return mixed

    def generate_track(self, num_bars=8):
        bar_samples = int(self.sr * (self.beat_ms * 4 / 1000))
        total_samples = bar_samples * num_bars
        track = np.zeros(total_samples)

        for bar in range(num_bars):
            start_idx = bar * bar_samples
            idx = random.choice([i for i in range(len(self.chords_pool)) if i != self.last_chord_idx])
            self.last_chord_idx = idx
            
            chord_wave = self._gen_tone(self.chords_pool[idx], self.beat_ms * 4)
            end_idx = start_idx + len(chord_wave)
            if end_idx <= total_samples:
                track[start_idx:end_idx] += chord_wave

            for beat in range(4):
                beat_start = start_idx + int(self.sr * (beat * self.beat_ms / 1000))
                
                if beat == 0:
                    hit = self._gen_drum("kick")
                    if beat_start + len(hit) < total_samples: track[beat_start:beat_start+len(hit)] += hit
                if beat == 2:
                    hit = self._gen_drum("snare")
                    if beat_start + len(hit) < total_samples: track[beat_start:beat_start+len(hit)] += hit
                if random.random() > 0.4:
                    hit = self._gen_drum("hihat")
                    if beat_start + len(hit) < total_samples: track[beat_start:beat_start+len(hit)] += hit

                if beat in [1, 3] and random.random() > 0.5:
                    melody_note = [f * 2 for f in self.chords_pool[idx]]
                    note_wave = self._gen_tone([random.choice(melody_note)], self.beat_ms, True)
                    if beat_start + len(note_wave) < total_samples: track[beat_start:beat_start+len(note_wave)] += note_wave

        track += np.random.normal(0, self.current_cfg["noise"], total_samples)
        
        indices = np.arange(total_samples)
        shift = 0.003 * np.sin(2 * np.pi * 0.4 * indices / self.sr)
        idx = np.clip(indices + shift * self.sr, 0, total_samples - 1).astype(np.int32)
        track = track[idx]
        
        track[:100] *= np.linspace(0, 1, 100)
        track[-100:] *= np.linspace(1, 0, 100)

        return track.astype(np.float32)

# --- 系統控制器 ---
engine = WebLofiEngine()
audio_ctx = None
is_playing = False
active_source = None
active_gain = None  
playback_start_time = 0.0 
current_mode_text = "MIDNIGHT" # 🌟 新增：系統現在會記住目前的文字狀態

def init_audio():
    global audio_ctx
    if audio_ctx is None:
        audio_ctx = js.AudioContext.new()

def start_playback():
    global active_source, active_gain, playback_start_time, is_playing
    
    data = engine.generate_track(num_bars=8)
    js_array = to_js(data)
    
    buffer = audio_ctx.createBuffer(1, len(data), 44100)
    buffer.copyToChannel(js_array, 0)
    
    source = audio_ctx.createBufferSource()
    source.buffer = buffer
    source.loop = True 
    
    gain = audio_ctx.createGain()
    gain.gain.value = 1.0
    
    lpf = audio_ctx.createBiquadFilter()
    lpf.type = "lowpass"
    lpf.frequency.value = engine.current_cfg["filter"]
    
    source.connect(gain)
    gain.connect(lpf)
    lpf.connect(audio_ctx.destination)
    
    source.start()
    active_source = source
    active_gain = gain
    playback_start_time = audio_ctx.currentTime 
    is_playing = True

def queue_next_mode():
    global active_source, active_gain, playback_start_time
    
    if not is_playing: return
    
    data = engine.generate_track(num_bars=8)
    js_array = to_js(data)
    
    buffer = audio_ctx.createBuffer(1, len(data), 44100)
    buffer.copyToChannel(js_array, 0)
    
    new_source = audio_ctx.createBufferSource()
    new_source.buffer = buffer
    new_source.loop = True 
    
    new_gain = audio_ctx.createGain()
    new_gain.gain.value = 0.0 
    
    lpf = audio_ctx.createBiquadFilter()
    lpf.type = "lowpass"
    lpf.frequency.value = engine.current_cfg["filter"]
    
    new_source.connect(new_gain)
    new_gain.connect(lpf)
    lpf.connect(audio_ctx.destination)
    
    bar_sec = (60.0 / engine.bpm) * 4.0
    elapsed = audio_ctx.currentTime - playback_start_time
    next_bar_idx = math.ceil(elapsed / bar_sec) 
    target_time = playback_start_time + next_bar_idx * bar_sec
    
    if target_time - audio_ctx.currentTime < 0.1:
        target_time += bar_sec
        
    fade_dur = 0.03 
    
    if active_gain:
        active_gain.gain.setValueAtTime(1.0, target_time - fade_dur)
        active_gain.gain.linearRampToValueAtTime(0.0, target_time)
        
    if active_source:
        active_source.stop(target_time + 0.1) 
        
    new_source.start(target_time)
    new_gain.gain.setValueAtTime(0.0, target_time)
    new_gain.gain.linearRampToValueAtTime(1.0, target_time + fade_dur)
    
    active_source = new_source
    active_gain = new_gain
    playback_start_time = target_time 

def update_ui_selection(active_id):
    for btn_id in ["#btn-midnight", "#btn-rainy", "#btn-cafe"]:
        el = document.querySelector(btn_id)
        if el: 
            if btn_id == active_id:
                el.classList.add("bg-white", "text-gray-900", "scale-105", "font-bold", "shadow-lg")
                el.classList.remove("bg-white/10", "bg-white/30", "text-white", "border-white/30")
            else:
                el.classList.add("bg-white/10", "border-white/30", "text-white")
                el.classList.remove("bg-white", "text-gray-900", "scale-105", "font-bold", "shadow-lg")

# --- 事件監聽器 ---

@when("click", "#play-btn")
def toggle_play(event):
    global is_playing, active_source, current_mode_text
    init_audio()
    
    btn = document.querySelector("#play-btn")
    if not is_playing:
        audio_ctx.resume()
        start_playback()
        btn.innerText = "STOP"
        btn.classList.add("bg-red-500", "text-white")
        btn.classList.remove("bg-white", "text-gray-900")
    else:
        is_playing = False
        if active_source is not None:
            try: active_source.stop()
            except: pass
            active_source = None
        audio_ctx.suspend()
        btn.innerText = "START"
        btn.classList.remove("bg-red-500", "text-white")
        btn.classList.add("bg-white", "text-gray-900")
        
    document.querySelector("#chord-display").innerText = current_mode_text

@when("click", "#btn-midnight")
def set_midnight(event):
    global current_mode_text
    current_mode_text = "Midnight"  # 🌟 改回溫和的首字母大寫
    engine.current_cfg = {"filter": 400, "noise": 0.002}
    update_ui_selection("#btn-midnight")
    document.querySelector("#chord-display").innerText = current_mode_text
    if is_playing: queue_next_mode()

@when("click", "#btn-rainy")
def set_rainy(event):
    global current_mode_text
    current_mode_text = "Rainy"  # 🌟 改回溫和的首字母大寫
    engine.current_cfg = {"filter": 1200, "noise": 0.02}
    update_ui_selection("#btn-rainy")
    document.querySelector("#chord-display").innerText = current_mode_text
    if is_playing: queue_next_mode()

@when("click", "#btn-cafe")
def set_cafe(event):
    global current_mode_text
    current_mode_text = "Cafe"  # 🌟 改回溫和的首字母大寫
    engine.current_cfg = {"filter": 3000, "noise": 0.005}
    update_ui_selection("#btn-cafe")
    document.querySelector("#chord-display").innerText = current_mode_text
    if is_playing: queue_next_mode()

def initialize_system():
    try:
        play_btn = document.querySelector("#play-btn")
        play_btn.innerText = "START"
        play_btn.disabled = False
        play_btn.classList.remove("opacity-50", "cursor-not-allowed")
        
        # 🌟 初始化時的文字與內部變數也統一改回
        global current_mode_text
        current_mode_text = "Midnight"
        document.querySelector("#chord-display").innerText = current_mode_text 
        update_ui_selection("#btn-midnight")
    except Exception as e:
        pass

initialize_system()