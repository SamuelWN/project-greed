SET @search = "%apple%";
/*   http://dev.mysql.com/doc/refman/5.0/en/pattern-matching.html   */

SELECT
	*
FROM
	stock
WHERE stock.company LIKE @search
	OR stock.symbol LIKE @search