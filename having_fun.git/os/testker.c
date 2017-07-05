#include<linux/init.h>
#include<linux/kernel.h>
#include<linux/module.h>
int Load()
{
printk(KERN_INFO  "Nik is trying to load module here!!!!!!!!!!!!!!!\n");
return 0;
}
void Exit()
{
printk(KERN_INFO "Nik is exiting  from here\n");
}
module_init(Load);
module_exit(Exit);

