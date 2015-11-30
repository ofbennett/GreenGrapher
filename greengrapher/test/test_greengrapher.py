import numpy as np
import requests
from matplotlib import image as img
from mock import patch, MagicMock
from nose.tools import assert_raises, assert_equal
from .. import command,greengraphertools

def test_example():
    assert_equal(1,1,msg='Here is my great message')

def test_construct_Map():
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


def test_green():

    with patch.object(requests,'get') as mock_get:
        with patch.object(img,'imread') as mock_imread:
            mock_map = greengraphertools.Map(111,222)
            not_green_array = np.ones([5,5,3])
            mock_map.pixels = not_green_array
            tmp = mock_map.green(1.1)
            all_false = np.zeros([5,5])
            outcome = np.array_equal(tmp,all_false)
            assert_equal(outcome,True)


#test_green()
