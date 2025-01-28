import os
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
from moviepy.config import change_settings

# Configurer ImageMagick si nécessaire
change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

# Étape 1 : Convertir le texte en audio
def text_to_audio(text, output_audio_path):
    try:
        tts = gTTS(text, lang='fr')
        tts.save(output_audio_path)
        print(f"Audio généré et sauvegardé : {output_audio_path}")
    except Exception as e:
        print(f"Erreur lors de la génération de l'audio : {e}")

# Étape 2 : Générer les sous-titres
def generate_subtitles(text, audio_duration):
    try:
        words = text.split()
        duration_per_word = audio_duration / len(words)
        subtitles = []
        current_time = 0
        line = []
        for word in words:
            line.append(word)
            if len(line) >= 8:  # Ajuster le nombre de mots par ligne
                subtitles.append({
                    "start": current_time,
                    "end": current_time + len(line) * duration_per_word,
                    "text": " ".join(line)
                })
                current_time += len(line) * duration_per_word
                line = []
        if line:  # Ajouter les mots restants
            subtitles.append({
                "start": current_time,
                "end": current_time + len(line) * duration_per_word,
                "text": " ".join(line)
            })
        print("Sous-titres générés avec succès.")
        return subtitles
    except Exception as e:
        print(f"Erreur lors de la génération des sous-titres : {e}")
        return []

# Étape 3 : Combiner l'audio avec la vidéo et ajouter les sous-titres
def combine_audio_video_with_subtitles(audio_path, video_path, output_path, subtitles):
    try:
        print("Chargement de la vidéo et de l'audio...")
        video = VideoFileClip(video_path).resize(height=720).subclip(0, 61)
        audio = AudioFileClip(audio_path).subclip(0, 61)
        video = video.set_audio(audio)  # Associe l'audio à la vidéo
        
        test_video = video.set_audio(audio)
        test_video.write_videofile("test_output.mp4", codec="libx264", audio_codec="aac")
        
        print("Ajout des sous-titres...")
        subtitle_clips = []
        for subtitle in subtitles:
            txt_clip = TextClip(
                subtitle["text"],
                fontsize=24,
                color='white',
                size=(video.w * 0.8, None),
                method='caption',
                bg_color='black'
            ).set_position(('center', 'bottom')).set_start(subtitle["start"]).set_duration(subtitle["end"] - subtitle["start"])
            subtitle_clips.append(txt_clip)

        print("Combinaison finale des clips...")
        final_video = CompositeVideoClip([video] + subtitle_clips).subclip(0, 61)
        final_video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=4,
            bitrate="5000k",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True
        )
        print(f"Vidéo finale générée avec succès : {output_path}")
    except Exception as e:
        print(f"Erreur lors de la combinaison audio/vidéo : {e}")


# Exemple d'utilisation
if __name__ == "__main__":
    try:
        text = ("Dans un petit village isolé, Hugo, un garçon curieux de dix ans, découvrit une clé ancienne en creusant "
                "près d’un arbre mort. Gravée d’un symbole étrange, elle semblait appeler à une aventure. Cette nuit-là, "
                "une lumière éthérée dansait au grenier de sa maison, comme une invitation. Hugo, serrant la clé dans sa main, "
                "monta les marches grinçantes. Là, il trouva un vieux coffre poussiéreux qu’il n’avait jamais remarqué auparavant. "
                "Tremblant d’excitation, il inséra la clé. Le coffre s’ouvrit dans un fracas, dévoilant un livre dont les pages "
                "brillaient d’une lumière dorée. En lisant les premières lignes, Hugo se retrouva transporté dans une forêt enchantée. "
                "Les arbres murmuraient son nom, et des créatures lumineuses dansaient autour de lui. Mais une voix grave interrompit "
                "l’euphorie. Tu as libéré un pouvoir ancien, Hugo. Utilise-le avec sagesse, car le monde en dépend. Hugo sentit une "
                "chaleur envahir sa main. La clé se mit à vibrer et à s’effacer lentement, jusqu’à disparaître complètement. Le livre, "
                "toujours ouvert, semblait attendre qu’il prenne une décision. Hugo prit une profonde inspiration et murmura Je promets "
                "de protéger ce pouvoir. D’un coup, la lumière s’intensifia et tout disparut. Il se retrouva dans son grenier, le livre "
                "fermé sur ses genoux. Mais cette fois, une phrase était gravée sur la couverture Quand le moment viendra, tu sauras quoi faire. "
                "Hugo sourit, déterminé. Il savait que son aventure ne faisait que commencer.")
        audio_path = "output_audio.mp3"
        video_path = "background_video.mp4"
        output_path = "final_video_with_subtitles.mp4"

        # Générer l'audio
        text_to_audio(text, audio_path)

        # Générer les sous-titres
        audio_duration = AudioFileClip(audio_path).duration
        subtitles = generate_subtitles(text, audio_duration)

        # Combiner audio, vidéo et sous-titres
        combine_audio_video_with_subtitles(audio_path, video_path, output_path, subtitles)
    except Exception as e:
        print(f"Erreur inattendue : {e}")
