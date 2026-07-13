import pytest
from dash import Dash
from app import app as dash_app

@pytest.fixture
def app() -> Dash:
    return dash_app

def test_header_present(dash_duo, app):
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal('h1', 'Soul Foods Sales Visualizer', timeout=5)
    header = dash_duo.find_element('h1')
    assert header.is_displayed()

def test_line_chart_present(dash_duo, app):
    dash_duo.start_server(app)
    chart = dash_duo.find_element('#sales-line-chart')
    assert chart is not None
    assert chart.is_displayed()

def test_region_picker_present(dash_duo, app):
    dash_duo.start_server(app)
    radio = dash_duo.find_element('#region-filter')
    assert radio is not None
    assert radio.is_displayed()
