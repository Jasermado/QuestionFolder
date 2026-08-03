from __future__ import annotations

import base64

from openai import OpenAI


class QuestionAnalyzer:
    def __init__(
        self,
        api_key: str,
        model: str,
        timeout_seconds: float = 90.0,
        max_output_tokens: int = 1200,
    ) -> None:
        self.client = OpenAI(api_key=api_key, timeout=timeout_seconds)
        self.model = model
        self.max_output_tokens = max_output_tokens

    def analyze_png(self, png_bytes: bytes, prompt: str) -> str:
        encoded = base64.b64encode(png_bytes).decode("utf-8")
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{encoded}",
                        },
                    ],
                }
            ],
            max_output_tokens=self.max_output_tokens,
        )
        output = response.output_text.strip()
        if not output:
            raise RuntimeError("The model returned an empty response.")
        return output
