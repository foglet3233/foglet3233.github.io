# ive used pygame but never turtle graphics so i used ai to help a little bit 
import turtle
screen = turtle.Screen()
screen.bgcolor("white")
screen.title("Drawing with Turtle graphics")
# create turtle
pen = turtle.Turtle()
# draw a triangle using a for loop
pen.color("blue")
pen.penup()
pen.goto(-100, 50) # starting pos for triangle
pen.pendown()
for _ in range(3):
 
pen.forward(100)
 
pen.left(120)
# draw a square using a loop
pen.color("green")
pen.penup()
pen.goto(100, 50)
pen.pendown()
side = 0
while side < 4:
 
pen.forward(100)
 
pen.right(90)
 
side += 1
# snowflake pattern (got a little help from chatgpt)
pen.penup()
pen.goto(0, -100) # Center the snowflake
pen.pendown()
pen.color("purple")
for _ in range(8): # Create 8 branches of the snowflake (diagonals included)
 
pen.forward(50)
 
pen.backward(50)
 
pen.right(45) # Adjusted to 45 degrees to ensure all diagonals are drawn
# hide the turtle and display the design
pen.hideturtle()
screen.mainloop()
