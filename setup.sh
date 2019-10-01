#!/usr/bin/env bash
cp splash.service /etc/systemd/system/splash.service && \
    systemctl daemon-reload && \
    systemctl start splash.service && \
    systemctl status splash.service

