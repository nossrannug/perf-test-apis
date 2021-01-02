if ! curl --output /dev/null --silent --fail http://localhost:8000/health; then
  echo "🕰️ Waiting for the api to start"
  echo ""
  until $(curl --output /dev/null --silent --fail http://localhost:8000/health); do
    printf '.'
    sleep 2
  done
  echo ""
fi
