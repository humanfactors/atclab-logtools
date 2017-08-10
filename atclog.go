package main

import (
	"fmt"
	"github.com/golang/example/stringutil"
	"io/ioutil"
	"regexp"
)

func main() {
	filecontents := textreader()
	match, _ := regexp.MatchString("atc", filecontents) // This tests whether a pattern matches a string.
	fmt.Println(match)
}

func textreader() string {
	f, err := ioutil.ReadFile("atc.xml") // just pass the file name
	if err != nil {
		fmt.Print(err)
	}
	filecontents := string(f) // convert content to a 'string'
	fmt.Println(filecontents) // print the content as a 'string'
	return string(filecontents)
}
