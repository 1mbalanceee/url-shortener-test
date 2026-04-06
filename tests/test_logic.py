import pytest

@pytest.mark.asyncio
async def test_shorten_and_redirect(async_client):
    # 1. Shorten a URL
    original_url = "https://fastapi.tiangolo.com/"
    response = await async_client.post("/shorten", json={"url": original_url})
    assert response.status_code == 200
    data = response.json()
    assert "short_id" in data
    short_id = data["short_id"]

    # 2. Check duplicate handles correctly and returns the same id
    response2 = await async_client.post("/shorten", json={"url": original_url})
    assert response2.status_code == 200
    assert response2.json()["short_id"] == short_id

    # 3. Request redirection with short_id (clicks should increment!)
    redirect_resp = await async_client.get(f"/{short_id}", follow_redirects=False)
    assert redirect_resp.status_code == 302
    assert redirect_resp.headers["location"] == original_url

    # 4. Check stats for clicks = 1
    stats_resp = await async_client.get(f"/stats/{short_id}")
    assert stats_resp.status_code == 200
    stats_data = stats_resp.json()
    assert stats_data["clicks"] == 1
    assert stats_data["original_url"] == original_url

@pytest.mark.asyncio
async def test_not_found_handling(async_client):
    # 1. Attempt to redirect nonexistent
    response = await async_client.get("/nonexistent123")
    assert response.status_code == 404
    assert response.json() == {"detail": "Short URL not found"}

    # 2. Attempt to get stats for nonexistent
    stats_response = await async_client.get("/stats/nonexistent123")
    assert stats_response.status_code == 404
    assert stats_response.json() == {"detail": "Short URL not found"}
