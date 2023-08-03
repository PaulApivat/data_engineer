import polars as pl
import time

"""MISSING: Storing data locally instead of github

ethereum_contracts__v1_0_0__00000000_to_00999999.parquet        ethereum_contracts__v1_0_0__09000000_to_09999999.parquet
ethereum_contracts__v1_0_0__01000000_to_01999999.parquet        ethereum_contracts__v1_0_0__10000000_to_10999999.parquet
ethereum_contracts__v1_0_0__02000000_to_02999999.parquet        ethereum_contracts__v1_0_0__11000000_to_11999999.parquet
ethereum_contracts__v1_0_0__03000000_to_03999999.parquet        ethereum_contracts__v1_0_0__12000000_to_12999999.parquet
ethereum_contracts__v1_0_0__04000000_to_04999999.parquet        ethereum_contracts__v1_0_0__13000000_to_13999999.parquet
ethereum_contracts__v1_0_0__05000000_to_05999999.parquet        ethereum_contracts__v1_0_0__14000000_to_14999999.parquet
ethereum_contracts__v1_0_0__06000000_to_06999999.parquet        ethereum_contracts__v1_0_0__15000000_to_15999999.parquet
ethereum_contracts__v1_0_0__07000000_to_07999999.parquet        ethereum_contracts__v1_0_0__16000000_to_16799999.parquet
ethereum_contracts__v1_0_0__08000000_to_08999999.parquet        

"""

# Measuring Wall time
start_wall_time = time.time()

# Measuring CPU time
start_cpu_time = time.process_time()

ethereum_contracts_df = pl.scan_parquet('*.parquet')

result = (
    ethereum_contracts_df.select('contract_address', 'init_code')
    .filter(pl.col('init_code').bin.contains(bytes.fromhex('a165767970657283')))
    .with_columns(
        pl.col('contract_address').bin.encode('hex'),
        pl.col('init_code')
        .bin.encode('hex')
        .str.extract(r'a165767970657283(.{6})', 1),
    )
    .collect()
)

# End measurement for Wall time
end_wall_time = time.time()

# End measurement for CPU time
end_cpu_time = time.process_time()

print(result)
print("Wall time taken: {} seconds".format(end_wall_time - start_wall_time))
print("CPU time taken: {} seconds".format(end_cpu_time - start_cpu_time))
