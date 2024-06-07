# Compilation instructions

## Debug

### Compilation of a debug version

`python -m buildozer -v android debug`

### Launch the debug version on a device connected to the computer

`python -m buildozer -v android deploy run logcat | grep python`

## Release

### Creation of the app signing key

```bash
keytool -genkey -v -keystore ~/keystores/Linconym.keystore -alias Linconym -keyalg RSA -keysize 2048 -validity 10000
keytool -importkeystore -srckeystore ~/keystores/Linconym.keystore -destkeystore ~/keystores/Linconym.keystore -deststoretype pkcs12
```

### Compilation of a release version

```bash
export P4A_RELEASE_KEYALIAS="Linconym"
export P4A_RELEASE_KEYSTORE=~/keystores/Linconym.keystore
export P4A_RELEASE_KEYSTORE_PASSWD=
export P4A_RELEASE_KEYALIAS_PASSWD=
python -m buildozer android release
```

## Bug fix

### Java Heap Space error

`export GRADLE_OPTS="-Xms1724m -Xmx5048m -Dorg.gradle.jvmargs='-Xms1724m -Xmx5048m'"`

## IOS

### Before creating the project

`toolchain build kivy`

Warning: https://github.com/kivy/kivy-ios/issues/513

### Create the Xcode project

`toolchain create Linconym /Users/lisecreusy/Documents/Paul/Linconym`

### Open the Xcode project

`open linconym-ios/linconym.xcodeproj`

Warning after the install of firebase using `pod install`, the following command should be used.

`open linconym-ios/Linconym.xcworkspace`

### Add a library to Xcode

`toolchain build numpy`

### Update the Xcode project

This is only useful when new packages must be added. Code modifications are automatically taken into account.

`toolchain update linconym-ios`