bert-serving-start -model_dir chinese_L-12_H-768_A-12 -num_worker=4

mysql -h localhost -u zy -p

SELECT column_name, column_comment
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_schema = 'alidb'
  AND table_name = 'user_role'
  AND column_name = 'id';


SELECT column_name, column_comment FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = 'alidb' AND table_name = 'user_role';

