[Setup]
AppName=MKS Support Center
AppVersion=1.2.4
DefaultDirName={localappdata}\MKS Support Center
DefaultGroupName=MKS Support Center
OutputBaseFilename=MKS_Support_Center_Installer
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

OutputDir=I:\test\update
SetupIconFile=I:\test\update\icon\logo1.ico
WizardImageFile=I:\test\update\icon\setupimage.bmp
WizardSmallImageFile=I:\test\update\icon\smallimage.bmp

[Files]
Source: "D:\Flask\templates\Flask\templates\build\mks_support_centerX64_3.11\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "I:\it share\test\update\version.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Flask\static\images\logo2.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Flask\static\images\images.jpeg"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Flask\close_app.bat"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{commondesktop}\MKS Support Center"; Filename: "{app}\MKS_Support_Center.exe"; IconFilename: "{app}\logo2.ico"
Name: "{userstartup}\MKS Support Center"; Filename: "{app}\MKS_Support_Center.exe"; Tasks: startup

[Tasks]
Name: "startup"; Description: "Run MKS Support Center at startup"; GroupDescription: "Additional Options"; Flags: unchecked

[Run]
Filename: "{app}\MKS_Support_Center.exe"; Description: "Launch MKS Support Center"; Flags: nowait postinstall skipifsilent runascurrentuser
Filename: "{app}\MKS_Support_Center_main.exe"; Description: "Launch MKS Support Center Main"; Flags: nowait postinstall skipifsilent runascurrentuser

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"; ValueType: string; ValueData: "~ RUNASINVOKER DISABLEUACVIRTUALIZATION"; Flags: uninsdeletevalue; ValueName: "{app}\MKS_Support_Center.exe"
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"; ValueType: string; ValueData: "~ RUNASINVOKER DISABLEUACVIRTUALIZATION"; Flags: uninsdeletevalue; ValueName: "{app}\MKS_Support_Center_main.exe"

[Code]
procedure CreateStartupTask;
var
  Shell: Variant;
begin
  // ใช้ PowerShell เพื่อสร้าง Task ที่รันแอปพลิเคชันด้วยสิทธิ์ Admin
  Shell := CreateOleObject('WScript.Shell');
  Shell.Run('powershell.exe -Command "Register-ScheduledTask -TaskName ''MKS_Support_Center_AdminTask'' ' +
            '-Trigger (New-ScheduledTaskTrigger -AtLogon) ' +
            '-Action (New-ScheduledTaskAction -Execute ''{app}\MKS_Support_Center.exe'') ' +
            '-Principal (New-ScheduledTaskPrincipal -UserId SYSTEM -LogonType ServiceAccount -RunLevel Highest) ' +
            '-Settings (New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable) ' +
            '-RunLevel Highest -Force"', 0, True);
end;

procedure DisableUACForApp;
var
  Shell: Variant;
begin
  // ปิด UAC virtualization เฉพาะสำหรับแอปพลิเคชันนี้
  Shell := CreateOleObject('WScript.Shell');
  Shell.RegWrite('HKCU\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers\' + ExpandConstant('{app}\MKS_Support_Center.exe'), '~ RUNASINVOKER DISABLEUACVIRTUALIZATION', 'REG_SZ');
  Shell.RegWrite('HKCU\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers\' + ExpandConstant('{app}\MKS_Support_Center_main.exe'), '~ RUNASINVOKER DISABLEUACVIRTUALIZATION', 'REG_SZ');
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // สร้าง Task ที่จะรันแอปพลิเคชันในสิทธิ์ Admin โดยไม่แสดง UAC
    CreateStartupTask;

    // ปิด UAC virtualization สำหรับแอปพลิเคชันนี้
    DisableUACForApp;
  end;
end;
