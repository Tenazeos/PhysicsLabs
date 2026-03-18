import pytest

from labs.magnetic_trap.models import SegmentedRing


@pytest.fixture(params=[1, 10, 100])
def ring(request) -> SegmentedRing:
    radius = request.param
    return SegmentedRing(
        segment_count=100,
        radius=radius,
        z_cord=0,
    )
