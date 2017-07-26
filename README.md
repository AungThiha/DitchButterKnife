For some reasons, you might want to ditch ButterKnife but you feel like it's a lot of work because you have a lot of ButterKnife code in your codebase. This script will do 90% of the work for you in seconds. The script will recursively walk through all the folders of the directory you specify and will edit all the java class file in all of them. I said 90% because you will find a few minor errors but worry not, those minor errors can be fixed easily.

### Requirements

* Python3

### How to use

"support_library_version_number" is optional and you can only specify 26 for it. Support Library 26 removes the trouble of typecasting the views. By the time I wrote this script, it's still in beta. That's why I added this option.

* $ python run.sh path support_library_version_number

### Example

* $ python run.sh ~/Projects/SampleApp/app/src/main/java/com/aung/sample 26

### What doesn't work
* If a java class file has one or more inner classes, you will have some minor errors that you need to fix manually
* This script doesn't support OnClick binding