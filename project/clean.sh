#!/bin/bash

sudo -u postgres psql -f clean.sql
sudo -u postgres psql -f rebuild.sql student