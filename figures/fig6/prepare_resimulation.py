import shutil
import os
import csv


def prepare_run(fluctuations, cost, counter):
    if fluctuations:
        dirname = "run_{}".format(counter)
        write_batch_file(dirname, [str(idx) for idx in fluctuations])
        shutil.copy("resimulate.py", dirname)
        shutil.copy("peaks.csv", dirname)


def write_batch_file(dirname, fluctuations_str):
    os.mkdir(dirname)
    with open("batch_template.sh") as f:
        template = f.read()
    exec_line = "python resimulate.py " + " ".join(fluctuations_str)
    batch_file = template.replace("exec_line", exec_line)
    with open(os.path.join(dirname, dirname + ".sh"), "w") as f:
        f.write(batch_file)


def prepare_resim(max_cost, t2h):
    log = open("prepare_resimulation.log", "w")
    cost = 0
    extremes_file = open("peaks.csv", mode="r")
    fluct_iterator = csv.reader(extremes_file, delimiter=",")
    fluctuations = []
    for counter, fluct in enumerate(fluct_iterator):
        dirname, init_file, nb_timesteps, peak, value = fluct
        nb_timesteps = int(nb_timesteps)
        if nb_timesteps > max_cost:
            msg = "Leaving out fluctuation no {:d} because its " \
            "resimulation cost is greater than max cost (was {:.1f}h)".format(
                counter, nb_timesteps / t2h / 60
            )
            log.write(msg+"\n")
        else:
            if cost + nb_timesteps > max_cost:
                prepare_run(fluctuations, cost, counter - 1)
                cost = 0
                fluctuations.clear()
            fluctuations.append(counter)
            cost = cost + nb_timesteps
    extremes_file.close()
    log.close()
    # Remainder
    prepare_run(fluctuations, cost, "end")


if __name__ == "__main__":
    base_duration = 1*60+50
    base_cost = 600211

    max_duration = 6*60
    t2h = base_cost / base_duration
    max_cost = int(t2h * max_duration)

    prepare_resim(max_cost, t2h)
