# shepherd-fast
A rewrite of shepherd using python 3.9 and FastAPI.

Reasons for a re-write:
 1. 1.0 was designed to serve webpages we now use shepherd as an API. This fundemental different use means that large sections of the code are now obsolete and there is clutter and assumptions based on how things used to be
 2. We would like to intergrate the robot lib in Shepherd to be persistant. This is again a different fundemental assumption
 3. Cleaning up shepherd and re-factoring is probally about as much work as just re-writing it now we know what we want.
 4. The calling convention for the robot lib are *weird* this alone is not a bad thing but it does make maintance harder.
 5. It is not clear what is meant to be in the API and what is just hacked functionality
 6. There is no unit testing

Reasons against the re-write:
 1. Shepherd 1.0 has been extensively battle tested
 2. A re-write might be a waste of developement effort
 3. All of the problems can be solved with a refactor

I (Edwin) think that a prototype re-write should at least be tried to see how hard it is mainly for 2, 5 and 6.
