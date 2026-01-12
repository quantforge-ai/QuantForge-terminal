@echo off
REM Quick test for auth endpoint
echo Testing if /auth/register exists...
curl -X GET http://localhost:8000/auth/register
echo.
echo.
echo Testing if /docs endpoint exists...
curl -X GET http://localhost:8000/docs -s -o nul -w "HTTP Status: %%{http_code}"
echo.
