/* Native harness for the gam4988 web core (site/vendor/gam4988/src/web_main.c):
   boots a .gam, presses keys and dumps frames as PGM (green channel).
   Script lines: "<frame> <key hex>" queues a key before that frame, "<frame> shot" dumps it. */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
int web_init(const uint8_t*,size_t); int web_load_game(const uint8_t*,size_t);
int web_run_frame(void); void web_keydown(uint8_t); uint8_t* web_get_framebuffer_rgba(void);
int web_get_fb_width(void); int web_get_fb_height(void);
static uint8_t* slurp(const char*p,size_t*n){FILE*f=fopen(p,"rb");if(!f){perror(p);exit(1);}fseek(f,0,2);*n=ftell(f);rewind(f);uint8_t*b=malloc(*n);fread(b,1,*n,f);fclose(f);return b;}
int main(int c,char**v){if(c!=5){fprintf(stderr,"usage: shot bios gam out_prefix script\n");return 2;}
 size_t bn,gn;uint8_t*b=slurp(v[1],&bn),*g=slurp(v[2],&gn);
 printf("init %d\n",web_init(b,bn)); printf("load %d\n",web_load_game(g,gn));
 FILE*s=fopen(v[4],"r");if(!s){perror(v[4]);return 1;}int fr=0,at;char w[32];int W=web_get_fb_width(),H=web_get_fb_height();
 while(fscanf(s,"%d %31s",&at,w)==2){while(fr<at){web_run_frame();fr++;}
  if(w[0]=='s'){char fn[512];snprintf(fn,512,"%s_%06d.pgm",v[3],fr);FILE*o=fopen(fn,"wb");fprintf(o,"P5 %d %d 255\n",W,H);uint8_t*p=web_get_framebuffer_rgba();for(int i=0;i<W*H;i++)fputc(p[4*i+1],o);fclose(o);}
  else web_keydown((uint8_t)strtol(w,0,16));}
 return 0;}
