import numpy as np

def normal1(wave): #this method will ignore amplitude but still persist the waveform into 1-100 
	print 'original wave: '+str(wave)

	diff = np.diff(wave)

	print 'diff: '+ str(wave)

	abs_diff = np.abs(diff)
	sum_abs_diff = np.sum(abs_diff)
	times = float(100)/sum_abs_diff

	compressed_wave = [wave[0]]
	n=0
	for ele in wave:
		if n == len(wave)-1:
			break
		else:
			compressed_wave.append(compressed_wave[n]+diff[n]*times)
		n = n+1

	average = np.average(compressed_wave)
	shifted_compressed_wave = []
	for ele in compressed_wave:
		shifted_compressed_wave.append(ele-average)

	return shifted_compressed_wave


def best_shift(goal_wave, test_wave):
	
	nm_goal_wave = normal1(goal_wave)
	print "salse:"+str(nm_goal_wave)
	nm_test_wave = normal1(test_wave)
	print "test:"+str(nm_test_wave)
	each_round_score = []

	for n in range(0,len(goal_wave)-1):
		each_round_score.append(0)

		for test in nm_test_wave[0:len(nm_test_wave)-1-n]:
			for goal in nm_goal_wave[n:len(nm_test_wave)-1]:
				each_round_score[n]+=((goal-test)/(len(goal_wave)-n))*((goal-test)/(len(goal_wave)-n))

	return each_round_score
			
