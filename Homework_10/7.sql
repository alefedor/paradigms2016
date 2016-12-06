select Country.Name from Country
inner join City on Country.Code = City.CountryCode
group by Country.Name
having Country.Population > 2 * sum(City.Population)
order by Country.Name;