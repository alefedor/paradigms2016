select City.Name
from Country inner join Capital
on Country.Code = Capital.CountryCode
inner join City 
on Capital.CityId = City.id and Capital.CountryCode = Country.Code
where Country.Name like "Malaysia";