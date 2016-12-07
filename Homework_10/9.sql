select L.Year, R.Year, Country.Name, ((R.Rate - L.Rate) / (R.Year - L.Year))
from Country
inner join LiteracyRate L on Country.Code = L.CountryCode
inner join LiteracyRate R on Country.Code = R.CountryCode
inner join LiteracyRate M 
on Country.Code = M.CountryCode and L.Year <= M.Year and M.Year < R.Year
group by Country.Name, L.Year, R.Year
having count(distinct M.Year) = 1
order by ((R.Rate - L.Rate) / (R.Year - L.Year)) desc;