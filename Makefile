install:
	cd apps/api && uv sync
	cd apps/web && npm install

spark:
	docker compose up -d spark-connect

api:
	cd apps/api && uv run uvicorn main:app --reload --port 8000

web:
	cd apps/web && npm run dev

seed:
	@for problem in \
		packages/problems/group_by_basics \
		packages/problems/find_duplicates \
		packages/problems/handling_nulls \
		packages/problems/filter_and_count \
		packages/problems/categorize_by_price \
		packages/problems/combine_tables \
		packages/problems/column_arithmetic \
		packages/problems/top_n_overall \
		packages/problems/string_basics \
		packages/problems/daily_sales \
		packages/problems/simple_inner_join \
		packages/problems/customers_no_orders \
		packages/problems/self_join_manager \
		packages/problems/full_outer_join \
		packages/problems/customers_bought_both \
		packages/problems/unsold_products \
		packages/problems/popular_product_category \
		packages/problems/multi_table_join \
		packages/problems/monthly_revenue \
		packages/problems/revenue_share \
		packages/problems/conditional_aggregation \
		packages/problems/count_distinct_day \
		packages/problems/first_last_event \
		packages/problems/pivot_attendance \
		packages/problems/customers_above_avg \
		packages/problems/remove_outliers \
		packages/problems/top_n_per_group \
		packages/problems/running_total \
		packages/problems/stock_price_change \
		packages/problems/next_purchase_date \
		packages/problems/rolling_average \
		packages/problems/salary_vs_dept_avg \
		packages/problems/percentile_rank \
		packages/problems/dense_rank_vs_rank \
		packages/problems/yoy_growth \
		packages/problems/top_customers_region \
		packages/problems/monthly_active_users \
		packages/problems/weekend_vs_weekday \
		packages/problems/days_between_events \
		packages/problems/active_subscriptions \
		packages/problems/late_deliveries \
		packages/problems/aggregate_tags \
		packages/problems/explode_tags \
		packages/problems/count_tags_per_product \
		packages/problems/filter_array \
		packages/problems/most_common_tag \
		packages/problems/merge_arrays \
		packages/problems/extract_email_domain \
		packages/problems/mask_pii \
		packages/problems/split_count_words \
		packages/problems/standardize_phones \
		packages/problems/sessionize_clickstream \
		packages/problems/consecutive_streaks \
		packages/problems/funnel_analysis \
		packages/problems/customer_loyalty \
		packages/problems/tally_election \
		packages/problems/ledger_reconciliation \
		packages/problems/top_n_tiebreak \
		packages/problems/cohort_retention \
		packages/problems/parse_json_column \
		packages/problems/flatten_structs \
		packages/problems/etl_job_stats \
		packages/problems/increasing_yoy_sales \
		packages/problems/scd_type2 \
		packages/problems/scd_type2_modelling; do \
		echo "Seeding $$problem..."; \
		cd $$problem && ../../../apps/api/.venv/bin/python reference.py && cd ../../..; \
	done

docker-full:
	docker compose up -d --build

validate:
	apps/api/.venv/bin/python scripts/validate_problems.py $(PROBLEM)

# ── Production ────────────────────────────────────────────────────────────────

SERVER ?= root@YOUR_SERVER_IP

backup-db:
	ssh $(SERVER) "docker exec api sqlite3 /app/data/spark_practice.db .dump" > backups/backup_$(shell date +%Y%m%d_%H%M).sql
	@echo "Backup saved to backups/"

restore-db:
	@echo "Usage: make restore-db FILE=backups/backup_YYYYMMDD_HHMM.sql"
	ssh $(SERVER) "docker exec -i api sqlite3 /app/data/spark_practice.db" < $(FILE)

logs:
	ssh $(SERVER) "docker compose -f docker-compose.prod.yml logs -f api"

.PHONY: install spark api web seed docker-full validate backup-db restore-db logs
