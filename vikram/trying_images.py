from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type":"text","text":"You are poetic , marketing manager of ABC fashions"},
        {"type": "text", "text": "use the image given"},
        {
          "type": "image_url",
          "image_url": {
            "url": "https://c7.alamy.com/comp/2EHP6B0/christmas-sale-poster-with-winter-holidays-festive-wreath-discount-price-offer-promo-banner-decorated-by-xmas-tree-and-holly-branch-snowflake-star-2EHP6B0.jpg",
            "detail": "high"
          },
        },
        {"type": "text", "text": "write a promotional SMS message, use the given image for context"},
        {"type": "text", "text": "keep the message max to 50 words , give 3 options"}
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0].message.content)
