#!/usr/bin/env bash

for PID in $(ps aux | grep /usr/bin/kvm | grep -v grep | awk '{ print $2 }'); do
  SOFT_LIMIT=$(cat /proc/${PID}/limits 2>/dev/null | grep "Max open files" | awk '{ print $4 }')
  HARD_LIMIT=$(cat /proc/${PID}/limits 2>/dev/null | grep "Max open files" | awk '{ print $5 }')
  echo "PID ${PID} opened files: $(ls -1 /proc/${PID}/fd 2>/dev/null | wc -l)/${SOFT_LIMIT}/${HARD_LIMIT}"
done

#!/usr/bin/env bash

for PID in $(ps aux | grep /usr/bin/kvm | grep -v grep | awk '{ print $2 }'); do
  SOFT_LIMIT="1048576"
  HARD_LIMIT="2097152"
  echo "Changing the limits for PID ${PID}"
  prlimit --nofile=${SOFT_LIMIT}:${HARD_LIMIT} --pid ${PID}
done
