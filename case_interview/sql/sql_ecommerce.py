
import sqlite3
conn = sqlite3.connect('../raw_data/sql/ecommerce.sqlite')
db=conn.cursor()

def order_rank_per_customer(db):

    query = """
        SELECT
            o.OrderID ,
            o.CustomerID ,
            o.OrderDate ,
            Rank() over(
                PARTITION by o.CustomerID
                ORDER by o.OrderDate
            ) as order_rank
        from Orders o
    """

    return db.execute(db).fetchall()

def order_cumulative_amount_per_customer(db):
    '''
    calculate the sum of per order
    groupby orderID
    sum over to get cumulative amount per customer
    '''
    query = """
    with table_1 as (select o.OrderID ,o.CustomerID ,o.OrderDate ,
					    round(sum(od.UnitPrice*od.Quantity),2) as order_amount
                    from Orders o
                    join OrderDetails od on od.OrderID = o.OrderID
                    group by o.OrderID)
    select OrderID,CustomerID ,OrderDate,
        sum(order_amount) over(
            PARTITION by CustomerID
            ORDER by OrderDate
        ) as cum_sum
    from table_1
    """

    return db.execute(query).fetchall()

def get_average_purchase(db):
    # return the average amount spent per order for each customer ordered by customer ID
    '''
    calculate the sum amount per order
    calculate the average amount, group by customer
    '''
    query = """
        with table_1 as (select o.OrderID ,o.CustomerID ,
                        sum(od.UnitPrice*od.Quantity) as order_amount
                    from Orders o
                    join OrderDetails od on od.OrderID = o.OrderID
                    group by o.OrderID )
        select CustomerID ,round(avg(order_amount),2) as avg_amount
        from table_1
        group by CustomerID
        order by CustomerID
    """
    return db.execute(query).fetchall()

def get_general_avg_order(db):
    # return the average amount spent per order
    query = """
    with table_1 as (select sum(od.UnitPrice*od.Quantity) as order_amount
				from Orders o
				join OrderDetails od on od.OrderID = o.OrderID
				group by o.OrderID )
    select round(avg(order_amount),2) as avg_amount
    from table_1
    """
    return db.execute(query).fetchone()[0]

def best_customers(db):
    # return the customers who have an average purchase greater than the general average purchase
    query = """
    with OrderValues as (
        SELECT od.OrderID ,sum(od.UnitPrice * od.Quantity) as amount
        from OrderDetails od
        group by od.OrderID
    ),
    GeneralValue as(
        SELECT round(avg(amount),2) as avg_amount
        from OrderValues ov
    ),
    CustomerValue as(
        select c.CustomerID ,round(avg(amount),2) as avg_amount
        from Customers c
        join Orders o on c.CustomerID = o.CustomerID
        join OrderValues ov on o.OrderID = ov.OrderID
        group by c.CustomerID
        order by c.CustomerID
    )
    SELECT CustomerValue.CustomerID,CustomerValue.avg_amount
    from CustomerValue
    where CustomerValue.avg_amount > (SELECT avg_amount from GeneralValue)
    order by CustomerValue.avg_amount DESC
    """

    return db.execute(query).fetchall()

def top_ordered_product_per_customer(db):
    # return the list of the top ordered product by each customer based on the total ordered amount in USD
    query="""
        WITH OrderProduct AS (
	        SELECT od.ProductID ,o.CustomerID ,ROUND(SUM(od.UnitPrice*od.Quantity),2) AS amount
	        FROM OrderDetails od
	        JOIN Orders o  ON od.OrderID = o.OrderID
	        GROUP BY od.ProductID, o.CustomerID
	        ORDER BY amount DESC
        )
        SELECT CustomerID,ProductID ,MAX(amount) AS TopProduct
        FROM OrderProduct
        GROUP BY CustomerID
        ORDER BY TopProduct DESC
    """
    return db.execute(query).fetchall()

def average_number_of_days_between_orders(db):
    # return the average number of days between two consecutive orders of the same customer
    query="""
        WITH DatedOrders AS(
            SELECT
	            o.OrderID ,o.CustomerID ,o.OrderDate ,
	            LAG(o.OrderDate,1,0) OVER(
		            PARTITION BY o.CustomerID
		            ORDER BY o.OrderDate
	            ) AS PreviousOrderDate
            FROM Orders o
        )
        SELECT ROUND(AVG(JULIANDAY(OrderDate)-JULIANDAY(PreviousOrderDate))) AS time_delta
        FROM DatedOrders
        WHERE PreviousOrderDate !=0
    """
    return int(db.execute(query).fetchone()[0])
