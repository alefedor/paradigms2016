select Country.Name, sum(City.Population>=1000000)
from Country inner join City
on Country.Code = City.CountryCode
group by Country.Name
order by sum(City.Population>=1000000) desc, Country.Name;