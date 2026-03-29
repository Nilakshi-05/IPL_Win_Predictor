mkdir -p ~/.streamlit/

cat <<EOF > ~/.streamlit/config.toml
[server]
port = ${PORT:-8501}
headless = true
enableCORS = false
enableXsrfProtection = false
address = "0.0.0.0"
EOF