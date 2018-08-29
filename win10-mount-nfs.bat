SET NFS_PATH="\\192.168.3.33\home\htdocs"
SET MOUNT_PATH="Z:"
SET USER="username"

REM # 安装 NFS client
REM #   dism 镜像路径 动作 动作参数
REM #   online 是指当前系统
dism /online /Enable-Feature /FeatureName:ServicesForNFS-ClientOnly /FeatureName:ClientForNFS-Infrastructure /FeatureName:NFS-Administration /NoRestart


REM # 修改默认的匿名UID/GID
(
echo Windows Registry Editor Version 5.00
echo 
echo [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\ClientForNFS\CurrentVersion\Default]
echo "AnonymousGID"=dword:00000000
echo "AnonymousUID"=dword:00000000
)>"clientfornfs.reg"
regedit /s .\clientfornfs.reg
nfsadmin client stop
nfsadmin client start


REM # 挂载到Z：
runas /noprofile /user:%USER% mount -o anon -o nolock -o casesensitive=yes %NSF_PATH% %MOUNT_PATH%




