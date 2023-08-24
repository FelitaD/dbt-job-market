CREATE OR REPLACE TEMPORARY TABLE tmp_receipt_data (
  receiptid    INTEGER
 ,ReceiptJson  VARIANT
) AS
SELECT $1 AS receiptid
      ,PARSE_JSON($2) AS ReceiptJson
  FROM VALUES
         (1, $${"products":[{"productDescription": "Descr1a", "Quantity": 10},{"productDescription": "Descr1b", "Quantity": 25}]}$$)
        ,(2, $${"products":[{"productDescription": "Descr2a", "Quantity": 15},{"productDescription": "Descr2b", "Quantity": 50}]}$$)
        ,(3, $${"products":[{"productDescription": "Descr3a", "Quantity":  5},{"productDescription": "Descr3b", "Quantity": 10}]}$$)
;
 
SELECT X.receiptid
      ,ARRAY_AGG(Y.VALUE:"productDescription"::VARCHAR) AS prod_descrs
      ,ARRAY_SIZE(prod_descrs) AS prod_descrs_size
  FROM tmp_receipt_data X
      ,LATERAL FLATTEN(input => ReceiptJson:"products") Y
 WHERE X.receiptid = 1
 GROUP BY X.receiptid
;