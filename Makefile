up:
	docker-compose up -d --build api

down:
	docker-compose down

logs:
	docker-compose logs -t -f api

rebuild:
	docker-compose up -d --build --force-recreate --no-deps

destroy:
	docker-compose down --rmi all -v --remove-orphans

test:
	docker-compose exec --workdir /home/appuser/tests -T api pytest -vv

coverage:
	docker-compose exec --workdir /home/appuser/tests -T api pytest -vv \
		--cov --cov-report=html

bash:
	docker-compose exec --workdir /home/appuser/api api /bin/bash
