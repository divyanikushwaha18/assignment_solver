# Assignment 1: Tools in Data Science

## 1. VS Code Version

**Question:** What is the output of code -s?

**Answer:**
```
C:\Users\Lenovo>code -s
Version:          Code 1.96.4 (cd4ee3b1c348a13bafd8f9ad8060705f6d4b9cba, 2025-01-16T00:16:19.038Z)
OS Version:       Windows_NT x64 10.0.19045
CPUs:             Intel(R) Core(TM) i3-7020U CPU @ 2.30GHz (4 x 2304)
Memory (System):  19.91GB (11.72GB free)
VM:               0%
Screen Reader:    no
Process Argv:     --crash-reporter-id af9cfa7e-6966-4c22-8280-8b9f7d4a71e1
GPU Status:       2d_canvas:                              enabled
                  canvas_oop_rasterization:               enabled_on
                  direct_rendering_display_compositor:    disabled_off_ok
                  gpu_compositing:                        enabled
                  multiple_raster_threads:                enabled_on
                  opengl:                                 enabled_on
                  rasterization:                          enabled
                  raw_draw:                               disabled_off_ok
                  skia_graphite:                          disabled_off
                  video_decode:                           enabled
                  video_encode:                           enabled
                  vulkan:                                 disabled_off
                  webgl:                                  enabled
                  webgl2:                                 enabled
                  webgpu:                                 enabled
                  webnn:                                  disabled_off

CPU %   Mem MB     PID  Process
    0      148    1732  code main
    0      114     876     gpu-process
    0      215    1296  window [1] (test.js - practice - Visual Studio Code)
    0       93    3540  fileWatcher [1]
    0       46    5036     utility-network-service
    0      144    7080  extensionHost [1]
    0      153    6204       electron-nodejs (tsserver.js )
    0      106   11364         electron-nodejs (typingsInstaller.js typesMap.js )
    0      113    7360       electron-nodejs (server.js )
    0      127   16932       electron-nodejs (tsserver.js )
    0       31    9004     crashpad-handler
    0      104    9116  ptyHost
    0        6   13288       conpty-agent
    0       70   16660       C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe -noexit -command "try { . \"c:\Users\Lenovo\AppData\Local\Programs\Microsoft VS Code\resources\app\out\vs\workbench\contrib\terminal\common\scripts\shellIntegration.ps1\" } catch {}"
    0      126   17192  shared-process

Workspace Stats:
|  Window (test.js - practice - Visual Studio Code)
|    Folder (practice): 1 files
|      File types: js(1)
|      Conf files:
```

## 2. HTTP Requests with uv

**Question:** What is the JSON output of the command uv run --with httpie -- https https://httpbin.org/get with the URL encoded parameter email set to 23f3000756@ds.study.iitm.ac.in?

**Answer:**
```json
{
    "args": {
        "email": "23f3000756@ds.study.iitm.ac.in"
    },
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "httpbin.org",
        "User-Agent": "HTTPie/3.2.4",
        "X-Amzn-Trace-Id": "Root=1-67924818-55fd761c0095804d4ee44835"
    },
    "origin": "106.219.89.4",
    "url": "https://httpbin.org/get?email=23f3000756%40ds.study.iitm.ac.in"
}
```

## 3. Run command with npx

**Question:** What is the output of the command npx -y prettier@3.4.2 README.md | sha256sum?

**Answer:**
```
19130fb88a7f92bccfa41338a5d5f2d085d4dbdbb321a5a3529724ced38c32fa
```

## 4. Use Google Sheets

**Question:** What is the result of =SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 3, 3), 1, 10)) in Google Sheets?

**Answer:** 165

## 5. Use Excel

**Question:** What is the result of =SUM(TAKE(SORTBY({6,10,8,15,3,13,6,6,1,10,2,15,10,1,0,11}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 4)) in Excel?

**Answer:** 31

## 6. Use DevTools

**Question:** What is the value in the hidden input?

**Answer:** qqsj05f7kq

## 7. Count Wednesdays

**Question:** How many Wednesdays are there in the date range 1985-12-29 to 2009-02-13?

**Answer:** 1207

## 8. Extract CSV from a ZIP

**Question:** What is the value in the "answer" column of the CSV file?

**Answer:** 70f51

## 9. Use JSON

**Question:** Sort this JSON array of objects by the value of the age field. In case of a tie, sort by the name field.

**Answer:**
```json
[{"name":"Frank","age":17},{"name":"Nora","age":21},{"name":"Alice","age":30},{"name":"David","age":31},{"name":"Oscar","age":31},{"name":"Henry","age":32},{"name":"Jack","age":35},{"name":"Emma","age":39},{"name":"Ivy","age":49},{"name":"Karen","age":49},{"name":"Charlie","age":62},{"name":"Mary","age":71},{"name":"Liam","age":73},{"name":"Bob","age":91},{"name":"Paul","age":91},{"name":"Grace","age":95}]
```

## 10. Multi-cursor edits to convert to JSON

**Question:** What's the result when you paste the JSON at tools-in-data-science.pages.dev/jsonhash and click the Hash button?

**Answer:** 64450c5825e58b380e6f556c0ff4fe1fc8c0e44f3bc9c6ea4ec306d5a217928e

## 11. CSS selectors

**Question:** Find all <div>s having a foo class in the hidden element below. What's the sum of their data-value attributes?

**Answer:** 223

## 12. Process files with different encodings

**Question:** What is the sum of all values associated with these symbols (› OR œ OR —) across all three files?

**Answer:** 41748

## 13. Use GitHub

**Question:** Enter the raw Github URL of email.json so we can verify it.

**Answer:** https://raw.githubusercontent.com/divyanikushwaha18/IITMassignments/refs/heads/master/email.json

## 14. Replace across files

**Question:** What does running cat * | sha256sum in that folder show in bash after replacing IITM with IIT Madras?

**Answer:** a6d711684bac20906e5d67a09048b6ebf0081fdaedb588212239929e44896766

## 15. List files and attributes

**Question:** What's the total size of all files at least 7461 bytes large and modified on or after Sat, 7 Jul, 2007, 2:42 pm IST?

**Answer:** 139208

## 16. Move and rename files

**Question:** What does running grep . * | LC_ALL=C sort | sha256sum in bash on that folder show after moving and renaming files?

**Answer:** d7a5eaac711761044c3b09460bf50ee91a01f9072f28d4e8dec226bca39a6a01  -

## 17. Compare files

**Question:** How many lines are different between a.txt and b.txt?

**Answer:** 50

## 18. SQL: Ticket Sales

**Question:** What is the total sales of all the items in the "Gold" ticket type?

**Answer:**
```sql
SELECT SUM(units * price) AS total_sales
FROM tickets
WHERE LOWER(TRIM(type)) = 'gold';
```
