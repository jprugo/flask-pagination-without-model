import pytest

tomorrow = "2022-03-03"

@pytest.mark.parametrize(
    "expected,date",
    [(200, '2022-03-01'), (204, tomorrow)]
)
def test_route1(
    mock_app,
    # monkeypatch,  # no needed
    mock_s3_resource,  # mock the bucket
    # parametrized
    expected, date
):
    url = f'/persona-raw-paginated?creationDate={date}&page=1?'

    app, client = mock_app

    response = client.get(url)

    assert response.status_code == expected

# Only 200 not 404


def test_route2(
    mock_app,
    # monkeypatch,  # no needed
    mock_s3_resource,  # mock the bucket
):
    url = '/persona/1'

    app, client = mock_app

    response = client.get(url)

    assert response.status_code == 200
