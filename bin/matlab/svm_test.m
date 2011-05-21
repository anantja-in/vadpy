function labels = svm_test(c, model_path)
    vars = load(model_path);
    model = vars.model;
    labels = svmpredict(rand(size(c,1),  1), c, model);
end
