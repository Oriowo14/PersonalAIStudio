import gradio as gr

from config import load_config
from core.content_composer import create_content_package


def create_content_composer_panel():

    config = load_config()

    video_provider = config.get(
        "video_provider",
        "local",
    )

    gr.Markdown(
        "# 🚀 AI Content Composer"
    )

    gr.Markdown(
        """
Turn one idea into a coordinated content package using
a local AI production planner.

**Idea → AI Plan → Image → Video → Voice → Music**
"""
    )

    # -------------------------------------------------
    # VIDEO PROVIDER STATUS
    # -------------------------------------------------

    if video_provider == "pollinations":

        gr.Markdown(
            """
### 🤖 AI Motion Video

Pollinations AI Motion is selected.

It can create genuine movement in the subject,
but requires available Pollen balance.
"""
        )

        video_duration_choices = [
            6,
            12,
            18,
            24,
        ]

        default_video_duration = 6

    else:

        gr.Markdown(
            """
### 🆓 Local Motion Video

Local Motion is currently selected.

It creates free cinematic camera movement.
For genuine body/object movement, select Pollinations
AI Motion when Pollen is available.
"""
        )

        video_duration_choices = [
            5,
            10,
            15,
            20,
        ]

        default_video_duration = 5

    # -------------------------------------------------
    # CONTENT IDEA
    # -------------------------------------------------

    prompt = gr.Textbox(
        label="💡 Content Idea",
        placeholder=(
            "Example: A young African entrepreneur "
            "building a successful technology company in Lagos."
        ),
        lines=6,
    )

    # -------------------------------------------------
    # CONTENT TYPE
    # -------------------------------------------------

    content_type = gr.Dropdown(
        choices=[
            "Story",
            "Advertisement",
            "Social Media",
            "Explainer",
            "Cinematic",
        ],
        value="Story",
        label="🎭 Content Type",
    )

    # -------------------------------------------------
    # IMAGE STYLE
    # -------------------------------------------------

    style = gr.Dropdown(
        choices=[
            "Realistic",
            "Fantasy",
            "Anime",
            "Cartoon",
            "Oil Painting",
            "Watercolour",
        ],
        value="Realistic",
        label="🖼 Image Style",
    )

    # -------------------------------------------------
    # VIDEO MOTION
    # -------------------------------------------------

    video_motion = gr.Dropdown(
        choices=[
            "Zoom In",
            "Zoom Out",
            "Pan Left",
            "Pan Right",
        ],
        value="Zoom In",
        label="🎬 Video Motion",
    )

    video_duration = gr.Dropdown(
        choices=video_duration_choices,
        value=default_video_duration,
        label="🎬 Video Duration (seconds)",
    )

    # -------------------------------------------------
    # VOICE
    # -------------------------------------------------

    voice = gr.Dropdown(
        choices=[
            "English Female",
            "English Male",
            "British Female",
            "British Male",
        ],
        value="English Female",
        label="🎙 Narration Voice",
    )

    # -------------------------------------------------
    # NARRATION TONE
    # -------------------------------------------------

    narration_tone = gr.Dropdown(
        choices=[
            "Professional",
            "Inspirational",
            "Dramatic",
            "Friendly",
        ],
        value="Friendly",
        label="📝 Narration Tone",
    )

    # -------------------------------------------------
    # MUSIC
    # -------------------------------------------------

    music_style = gr.Dropdown(
        choices=[
            "Cinematic",
            "Calm",
            "Upbeat",
            "Ambient",
        ],
        value="Cinematic",
        label="🎵 Music Style",
    )

    music_duration = gr.Dropdown(
        choices=[
            5,
            10,
            15,
            20,
            30,
        ],
        value=10,
        label="🎵 Music Duration (seconds)",
    )

    # -------------------------------------------------
    # GENERATE BUTTON
    # -------------------------------------------------

    generate_btn = gr.Button(
        "🚀 Create Complete Content",
        variant="primary",
    )

    status = gr.Markdown(
        "🟢 Ready"
    )

    # -------------------------------------------------
    # AI PRODUCTION PLAN
    # -------------------------------------------------

    gr.Markdown(
        "## 🧠 AI Production Plan"
    )

    plan_title = gr.Textbox(
        label="Title",
        interactive=False,
    )

    story_concept = gr.Textbox(
        label="Story Concept",
        lines=3,
        interactive=False,
    )

    main_subject = gr.Textbox(
        label="Main Subject",
        lines=2,
        interactive=False,
    )

    setting = gr.Textbox(
        label="Setting",
        lines=2,
        interactive=False,
    )

    visual_direction = gr.Textbox(
        label="Visual Direction",
        lines=4,
        interactive=False,
    )

    video_direction = gr.Textbox(
        label="AI Video Direction",
        lines=4,
        interactive=False,
    )

    music_direction = gr.Textbox(
        label="AI Music Direction",
        lines=4,
        interactive=False,
    )

    # -------------------------------------------------
    # IMAGE OUTPUT
    # -------------------------------------------------

    gr.Markdown(
        "## 🖼 Generated Image"
    )

    image = gr.Image(
        label="Generated Image",
        type="filepath",
        height=350,
    )

    # -------------------------------------------------
    # VIDEO OUTPUT
    # -------------------------------------------------

    gr.Markdown(
        "## 🎬 Generated Video"
    )

    video = gr.Video(
        label="Generated Video",
        height=350,
    )

    # -------------------------------------------------
    # VOICE OUTPUT
    # -------------------------------------------------

    gr.Markdown(
        "## 🎙 Generated Voice"
    )

    voice_audio = gr.Audio(
        label="Voice Narration",
        type="filepath",
    )

    # -------------------------------------------------
    # MUSIC OUTPUT
    # -------------------------------------------------

    gr.Markdown(
        "## 🎵 Generated Music"
    )

    music_audio = gr.Audio(
        label="Background Music",
        type="filepath",
    )

    # -------------------------------------------------
    # GENERATION FUNCTION
    # -------------------------------------------------

    def run_composer(
        prompt_value,
        content_type_value,
        style_value,
        video_motion_value,
        video_duration_value,
        voice_value,
        narration_tone_value,
        music_style_value,
        music_duration_value,
    ):

        if (
            not prompt_value
            or not prompt_value.strip()
        ):

            return (
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                None,
                None,
                None,
                None,
                "❌ Please enter a content idea.",
            )

        try:

            package = create_content_package(
                prompt=prompt_value,
                style=style_value,
                content_type=content_type_value,
                voice=voice_value,
                narration_tone=narration_tone_value,
                music_style=music_style_value,
                music_duration=music_duration_value,
                video_motion=video_motion_value,
                video_duration=video_duration_value,
            )

            plan = package["plan"]

            return (
                plan["title"],
                plan["story_concept"],
                plan["main_subject"],
                plan["setting"],
                plan["visual_direction"],
                plan["video_direction"],
                plan["music_direction"],
                package["image"],
                package["video"],
                package["voice"],
                package["music"],
                "✅ AI production plan and complete content package generated successfully!",
            )

        except Exception as error:

            return (
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                None,
                None,
                None,
                None,
                f"❌ {error}",
            )

    # -------------------------------------------------
    # BUTTON EVENT
    # -------------------------------------------------

    generate_btn.click(
        fn=run_composer,
        inputs=[
            prompt,
            content_type,
            style,
            video_motion,
            video_duration,
            voice,
            narration_tone,
            music_style,
            music_duration,
        ],
        outputs=[
            plan_title,
            story_concept,
            main_subject,
            setting,
            visual_direction,
            video_direction,
            music_direction,
            image,
            video,
            voice_audio,
            music_audio,
            status,
        ],
    )

    return (
        prompt,
        content_type,
        style,
        video_motion,
        video_duration,
        voice,
        narration_tone,
        music_style,
        music_duration,
        generate_btn,
        plan_title,
        story_concept,
        main_subject,
        setting,
        visual_direction,
        video_direction,
        music_direction,
        image,
        video,
        voice_audio,
        music_audio,
        status,
    )