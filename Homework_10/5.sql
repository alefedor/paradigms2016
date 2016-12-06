select GovernmentForm, sum(SurfaceArea)
from Country
group by Country.GovernmentForm
order by sum(SurfaceArea) desc
limit 1;