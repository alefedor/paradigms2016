select Country.Name, Country.Population, Country.SurfaceArea
from Country inner join City
on Country.Code = City.CountryCode
inner join Capital on Capital.CountryCode = Country.Code
group by Country.Name
having max(City.Population) = City.Population and City.Id <> Capital.CityId
order by (1.0 * Country.Population / Country.SurfaceArea) desc, Country.Name;
