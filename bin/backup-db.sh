#!/bin/bash
mysqldump -u jugiuser jugi > jugidb-$(date -I).sql
