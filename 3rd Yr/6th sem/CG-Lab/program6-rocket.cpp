New! Keyboard shortcuts … Drive keyboard shortcuts have been updated to give you first-letters navigation
#include<GL/glut.h>
#define BLAST_OFF 1
#define ROCKET 0
int flag = ROCKET;
float viewer[3] = {0,0,5};
float ty = 0;
int color = -1;
void rocket(){
	glColor3f(1,0,0);
	glPushMatrix();
	glTranslatef(0,1,0);
	glRotatef(-90,1,0,0);
	glutWireCone(0.9,1.5,10,10);
	glPopMatrix();

	glColor3f(1,1,0);
//body
	GLUquadricObj *quadratic;
	quadratic = gluNewQuadric();
	glPushMatrix();
	glTranslatef(0,-1.4,0);
	glRotatef(-90, 1,0,0);
	gluCylinder(quadratic,0.8f,0.8f,2.5f,32,32);

	glPopMatrix();

//wings - right

	glColor3f(0,0,1);
	glPushMatrix();
	glTranslatef(1,-1,0);
	glScalef(1,0.7,0.2);
	glRotatef(60, 0,0,1);
	glutSolidCube(1);
	glPopMatrix();

//wings - left

	
	glColor3f(0,0,1);
	glPushMatrix();
	glTranslatef(-1,-1,0);
	glScalef(1,0.7,0.2);
	glRotatef(-60, 0,0,1);
	glutSolidCube(1);
	glPopMatrix();

//fire
	
	glColor3f(1,0.5,0);
	glPushMatrix();
	glTranslatef(0,-2,0);
	glRotatef(-90,1,0,0);
	glutSolidCone(0.6,1.8,10,10);
	glPopMatrix();

}
void display(){
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glLoadIdentity();
	gluLookAt(viewer[0],viewer[1],viewer[2], 0,0,0, 0,1,0);
	if(flag == BLAST_OFF){
	glPushMatrix();
	glTranslatef(0,ty,0);
	glPushMatrix();// translate the whole rocket to the base
	glTranslatef(0,-3,0);
	rocket();
	glPopMatrix();
	ty+=0.1;// keep translating up
	glPopMatrix();
	glutPostRedisplay();

	} else if (flag == ROCKET){
	ty=0;
	glPushMatrix();// translate the whole rocket to the base
	glTranslatef(0,-3,0);
	rocket();
	glPopMatrix();
		
	}
	glutSwapBuffers();
}
void myinit(){
	glMatrixMode(GL_PROJECTION);
	glOrtho(-5,5,-5,5,2,20);
	glMatrixMode(GL_MODELVIEW);
}
void keys(unsigned char key, int x, int y){
	if (key=='x')viewer[0]+=0.2;
	else if(key=='X') viewer[0]-=0.2;
	else if(key=='y') viewer[1]+=0.2;
	else if(key=='Y') viewer[1]-=0.2;
	else if(key=='z') viewer[2]-=0.2;
	else if(key=='Z') viewer[2]+=0.2;

	//animation
	else if(key=='b') flag =BLAST_OFF;
	else if (key=='r') flag=ROCKET;
	glutPostRedisplay();
}
int main(int argc, char **argv) {
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH);
	glutInitWindowSize(500,500);
	glutCreateWindow("Animate 3D Rocket");
	myinit();
	glutDisplayFunc(display);
	glutKeyboardFunc(keys);
	glEnable(GL_DEPTH_TEST);
	glutMainLoop();
	return 0;
}
