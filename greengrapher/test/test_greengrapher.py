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
    #Tests the Greengraph.geolocate method with a mock and a simulated return value for London
    graph = greengraphertools.Greengraph('London', 'Oxford')
    with patch.object(graph.geocoder,'geocode') as mock_geocode:
        mock_geocode.return_value = [[0,(51.5073509, -0.1277583)],[0,0]]
        coordinates = graph.geolocate('London')
        mock_geocode.assert_called_with('London',exactly_one=False)
        assert_equal(coordinates,(51.5073509, -0.1277583))

def test_location_sequence():
    #Test the Greengraph.location_sequence method
    start = [1,1]
    end = [10,10]
    steps = 10
    expected = [[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10]]
    graph = greengraphertools.Greengraph('London', 'Oxford')
    result = graph.location_sequence(start,end,steps)
    outcome = np.array_equal(result,expected)
    assert_equal(outcome,True)

def test_green_between():
    #Test the Greengraph.green_between method with mocks
    steps = 10
    green_counts = [1,1,2,4,3,4,5,3,4,7]
    graph = greengraphertools.Greengraph('London', 'Oxford')
    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread') as mock_imread:
            with patch.object(graph, 'geolocate') as mock_geolocate:
                with patch.object(greengraphertools.Map,'count_green') as mock_count_green:
                    mock_geolocate.side_effect = [(51.5073509, -0.1277583),
                                                  (51.7520209, -1.2577263)]
                    mock_count_green.side_effect = green_counts
                    result = graph.green_between(steps)
                    assert_equal(result,green_counts)

def test_process():
    #Test command.process method using mocks
    from argparse import ArgumentParser
    from matplotlib import pyplot as plt
    begin = 'London'
    end = 'Oxford'
    steps = 10
    out = 'graph2.png'
    trial_data = 123

    class Expected(object):
        def __init__(self,begin,end,steps,out):
            self.begin = begin
            self.end = end
            self.steps = steps
            self.out = out

    expected = Expected(begin,end,steps,out)
    
    with patch.object(ArgumentParser,'parse_args') as mock_parse_args:
        mock_parse_args.return_value = expected
        with patch.object(greengraphertools.Greengraph,'green_between') as mock_green_between:
            mock_green_between.return_value = trial_data
            with patch.object(plt,'savefig') as mock_savefig:
                with patch.object(plt,'show') as mock_show:
                    with patch.object(plt,'plot') as mock_plot:
                        command.process()
                        mock_parse_args.assert_called_once
                        mock_green_between.assert_called_with(expected.steps)
                        mock_savefig.assert_called_with(expected.out)
                        mock_plot.assert_called_with(trial_data)
