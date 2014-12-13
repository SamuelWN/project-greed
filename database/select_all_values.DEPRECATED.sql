SET @p_id = 1;
SET @p_unixtime = 1417977956;


SELECT
    sub_portfolio_delta.unixtime AS unixtime,
    portfolio_cash_value(sub_portfolio_delta.id, sub_portfolio_delta.unixtime) AS cash_value,
    IFNULL(portfolio_competition_reserved_value(sub_portfolio_delta.id, sub_portfolio_delta.unixtime, false), 0) AS comp_value,
    IFNULL(GROUP_CONCAT(
		DISTINCT CONCAT(
			sub_portfolio_stocks.stock_symbol,
			"-",
			IFNULL(portfolio_stock_count(sub_portfolio_delta.id, sub_portfolio_delta.unixtime, sub_portfolio_stocks.stock_symbol), 0)
		)
        ORDER BY sub_portfolio_stocks.stock_symbol
		SEPARATOR '/'
	), "") AS stock_count
FROM sub_portfolio_delta
LEFT OUTER JOIN sub_portfolio_stocks
	ON sub_portfolio_delta.id = sub_portfolio_stocks.id
WHERE
	sub_portfolio_delta.id = @p_id
    AND CASE WHEN ISNULL(@p_unixtime)
			THEN true
			ELSE sub_portfolio_delta.unixtime <= @p_unixtime
		END
GROUP BY sub_portfolio_delta.id, sub_portfolio_delta.unixtime
;