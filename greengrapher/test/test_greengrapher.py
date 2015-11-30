'''
Unit tests for the greengrapher module
'''
import numpy as np
import requests
from matplotlib import image as img
from mock import patch, MagicMock
from nose.tools import assert_raises, assert_equal
from .. import command,greengraphertools

def test_construct_Map():
    #Tests the Map class constructor with a mocks to prevent interaction with the internet
    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread') as mock_imread:
            mock_map = greengraphertools.Map(111,222)
        mock_get.assert_called_with(
        "http://maps.googleapis.com/maps/api/staticmap?",
        params = {
        'sensor':'false',
        'zoom':10,
        'size':'400x400',
        'center':'111,222',
        'style':'feature:all|element:labels|visibility:off',
        'maptype':'satellite'})


def test_green_when_map_not_green():
    #Tests the Map.green() method when the map has no green pixels
    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread') as mock_imread:
            mock_map = greengraphertools.Map(111,222)
            not_green_array = np.ones([5,5,3])
            mock_map.pixels = not_green_array
            green_pixels = mock_map.green(1.1)
            all_false = np.zeros([5,5])
            outcome = np.array_equal(green_pixels,all_false)
            assert_equal(outcome,True)

def test_green_when_map_all_green():
    #Tests the Map.green() method when the map has all green pixels
    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread') as mock_imread:
            mock_map = greengraphertools.Map(111,222)
            green_array = np.zeros([5,5,3])
            green_array[:,:,1] = 1
            mock_map.pixels = green_array
            green_pixels = mock_map.green(1.1)
            all_true = np.ones([5,5])
            outcome = np.array_equal(green_pixels,all_true)
            assert_equal(outcome,True)

def test_count_green_when_map_not_green():
    #Tests the Map.count_green() method when the map has no green pixels
    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread') as mock_imread:
            mock_map = greengraphertools.Map(111,222)
            not_green_array = np.ones([5,5,3])
            mock_map.pixels = not_green_array
            green_pixel_count = mock_map.count_green(1.1)
            assert_equal(green_pixel_count,0)

def test_count_green_when_map_all_green():
    #Tests the Map.count_green() method when the map has all green pixels
    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread') as mock_imread:
            mock_map = greengraphertools.Map(111,222)
            green_array = np.zeros([5,5,3])
            green_array[:,:,1] = 1
            mock_map.pixels = green_array
            green_pixel_count = mock_map.count_green(1.1)
            assert_equal(green_pixel_count,25)

def test_show_green_when_map_not_green():
    #Tests the Map.show_green() method when the map has no green pixels
    from StringIO import StringIO
    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread') as mock_imread:
            mock_map = greengraphertools.Map(111,222)
            not_green_array = np.ones([5,5,3])
            mock_map.pixels = not_green_array
            with patch.object(img,'imsave') as mock_imsave:
                mock_map.show_green()
                test_array = np.zeros([5,5,3])
                calls = mock_imsave.call_args
                arg,kwrds = calls
                assert_equal({'format':'png'},kwrds)
                outcome = (np.array_equal(test_array, arg[0]) or np.array_equal(test_array, arg[1]))
                assert_equal(outcome,True)

def test_show_green_when_map_all_green():
    #Tests the Map.show_green() method when the map has all green pixels
    from StringIO import StringIO
    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread') as mock_imread:
            mock_map = greengraphertools.Map(111,222)
            green_array = np.zeros([5,5,3])
            green_array[:,:,1] = 1
            mock_map.pixels = green_array
            with patch.object(img,'imsave') as mock_imsave:
                mock_map.show_green()
                test_array = np.zeros([5,5,3])
                test_array[:,:,1] = 1
                calls = mock_imsave.call_args
                arg,kwrds = calls
                assert_equal({'format':'png'},kwrds)
                outcome = (np.array_equal(test_array, arg[0]) or np.array_equal(test_array, arg[1]))
                assert_equal(outcome,True)

def test_construct_Greengraph():
    #Tests the Greengraph class constructor
    graph = greengraphertools.Greengraph('London', 'Oxford')
    assert_equal(['London','Oxford'],[graph.start,graph.end])

def test_geolocate():
    #Tests the Greengraph.geolocate method with a mock
    graph = greengraphertools.Greengraph('London', 'Oxford')
    with patch.object(graph.geocoder,'geocode') as mock_geocode:
        mock_geocode.return_value = [[0,(51.5073509, -0.1277583)],[0,0]]
        coordinates = graph.geolocate('London')
        mock_geocode.assert_called_with('London',exactly_one=False)
        assert_equal(coordinates,(51.5073509, -0.1277583))
