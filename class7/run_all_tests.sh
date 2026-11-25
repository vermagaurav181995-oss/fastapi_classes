#!/usr/bin/env bash

cd "$(dirname "$0")" || exit 1

TEST_FOLDERS=(
  01_pytest_basics
  02_testclient_basics
  03_fixtures
  03_fixtures/without_fixture
  04_parametrize
  05_testing_auth
  06_dependency_overrides
  07_middleware_background
  08_coverage
  09_production_settings
  13_websocket_chat
  14_capstone/template
  14_capstone/example_task_manager
  practice
  practice/solutions
)

passed=()
failed=()

for folder in "${TEST_FOLDERS[@]}"; do
  echo
  echo "=================== $folder ==================="
  if (cd "$folder" && python -m pytest -q -p no:randomly); then
    passed+=("$folder")
  else
    failed+=("$folder")
  fi
done

echo
echo "=================== SUMMARY ==================="
for folder in "${passed[@]}"; do echo "  PASS  $folder"; done
for folder in "${failed[@]}"; do echo "  FAIL  $folder"; done
echo "${#passed[@]} passed, ${#failed[@]} failed (out of ${#TEST_FOLDERS[@]} folders)"

[ ${#failed[@]} -eq 0 ]
