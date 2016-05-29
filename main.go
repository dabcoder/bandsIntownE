package main

import (
    "encoding/json"
    "net/http"
    "strings"
)

func main() {

	http.HandleFunc("/bands/", func(w http.ResponseWriter, r *http.Request) {
		artist := strings.SplitN(r.URL.Path, "/", 3)[2]

		data, err := query(artist)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
        	return
		}

		w.Header().Set("Content-Type", "application/json; charset=utf-8")
		json.NewEncoder(w).Encode(data)
	})

	http.ListenAndServe(":8080", nil)
}

func query(artist string) (bandsData, error) {
	resp, err := http.Get("http://api.bandsintown.com/artists/" + artist + ".json?api_version=2.0&app_id=bitgoapp")
	if err != nil {
		return bandsData{}, err
	}

	defer resp.Body.Close()

	var b bandsData


	if err := json.NewDecoder(resp.Body).Decode(&b); err != nil {
        return bandsData{}, err
    }

    return b, nil
}

type bandsData struct {
	Name string `json:"name"`
	NumberEvents int `json:"upcoming_event_count"` 
}