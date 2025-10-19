#!/usr/bin/env python3
import asyncio

try:
    from playwright.async_api import async_playwright

    has_playwright = True
except ImportError:
    has_playwright = False
    import requests


async def test_api_with_playwright():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Set headers
        await page.set_extra_http_headers(
            {
                "X-Super-Client": "hc.dataknife.ai",
                "X-Super-Contact": "lee@fullmetal.dev",
            }
        )

        try:
            response = await page.goto(
                "https://api.helldivers2.io/api/v1/war/status", wait_until="load"
            )
            print(f"Status Code: {response.status}")
            content = await page.content()
            print("\nResponse Preview:")
            print(content[:500])
        except Exception as e:
            print(f"Error during navigation: {e}")
        finally:
            await browser.close()


def test_api_with_requests():
    headers = {
        "X-Super-Client": "hc.dataknife.ai",
        "X-Super-Contact": "lee@fullmetal.dev",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    try:
        response = requests.get(
            "https://api.helldivers2.io/api/v1/war/status", headers=headers, timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print("\nResponse Preview:")
        print(response.text[:500])
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if has_playwright:
        print("Using Playwright to bypass bot detection...")
        asyncio.run(test_api_with_playwright())
    else:
        print("Playwright not available, using requests...")
        test_api_with_requests()
