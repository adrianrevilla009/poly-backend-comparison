package main

import (
	"encoding/json"
	"net/http"
	"os"
	"strconv"
	"strings"
)

type Order struct {
	ID       int64   `json:"id"`
	Customer string  `json:"customer"`
	Total    float64 `json:"total"`
	Status   string  `json:"status"`
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"status":"UP"}`))
	})
	mux.HandleFunc("/orders/", func(w http.ResponseWriter, r *http.Request) {
		id, err := strconv.ParseInt(strings.TrimPrefix(r.URL.Path, "/orders/"), 10, 64)
		if err != nil || id < 0 {
			http.Error(w, `{"error":"bad id"}`, http.StatusBadRequest)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(Order{id, "c-" + strconv.FormatInt(id%100, 10), float64(id%1000) + 0.5, "NEW"})
	})
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	http.ListenAndServe(":"+port, mux)
}
