from openai import OpenAI
client = OpenAI()

response = client.images.generate(
  model="dall-e-3",
  prompt="A cool poster for ABC fashions brand's end of season sale,make it realistic with people wearing jeans and casual wear with lots of colour",
  n=1,
  size="1024x1024"
)
image_url = response.data[0].url
print(image_url)