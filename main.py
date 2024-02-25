import openai



response = openai.Image.create(
    model = "dall-e-3",
    prompt = "a brown cat sitting",
    size = "1024x1024",
    quality = "standard",
    n=1,
)




