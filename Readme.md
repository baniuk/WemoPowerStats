conda env export -n WemoPowerStats | Where-Object -FilterScript {$_ -notmatch '^prefix: '}

```bash
 python -m wemopowerstats -w .\client_secrets.json C:\Users\baniu\Downloads\tt homenewver
```
