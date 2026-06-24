import pytest
from angle_calculator import calculate_angle
from rep_counter import RepCounter
    
# angle tests
def test_angle_straight_arm():
    result = calculate_angle((0, 0), (1, 0), (2, 0))
    assert result == pytest.approx(180, abs=1)

def test_angle_right_angle():
    result = calculate_angle((0, 1), (0, 0), (1, 0))
    assert result == pytest.approx(90, abs=1)

def test_angle_acute():
    result = calculate_angle((0, 1), (0, 0), (1, 1))
    assert result == pytest.approx(45, abs=1)


# rep counter tests
def test_rep_counter_initialization():
    rep_counter = RepCounter(down_threshold=160, up_threshold=30)
    assert rep_counter.get_count() == 0
    assert rep_counter.get_state() == 'init'

def test_rep_counted_on_full_cycle():
    rep_counter = RepCounter(down_threshold=160, up_threshold=30)
    
    # Simulate a full rep cycle
    rep_counter.update(170)  # Move down
    rep_counter.update(20)   # Move up
    rep_counter.update(170)  # Move down again
    
    assert rep_counter.get_count() == 1
    assert rep_counter.get_state() == 'DOWN'

def test_rep_counter_no_count_if_not_full_cycle():
    rep_counter = RepCounter(down_threshold=160, up_threshold=30)
    
    # Simulate an incomplete rep cycle
    rep_counter.update(170)  # Move down
    rep_counter.update(20)   # Move up
    
    assert rep_counter.get_count() == 0
    assert rep_counter.get_state() == 'UP'

def test_rep_counter_reset():
    rep_counter = RepCounter(down_threshold=160, up_threshold=30)
    
    # Simulate a full rep cycle
    rep_counter.update(170)  # Move down
    rep_counter.update(20)   # Move up
    rep_counter.update(170)  # Move down again
    
    assert rep_counter.get_count() == 1
    
    # Reset the counter
    rep_counter.reset()
    
    assert rep_counter.get_count() == 0
    assert rep_counter.get_state() == 'init'